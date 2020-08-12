﻿/*
 * Copyright (C) 2010-2015 Nektra S.A., Buenos Aires, Argentina.
 * All rights reserved. Contact: http://www.nektra.com
 *
 *
 * This file is part of Deviare In-Proc
 *
 *
 * Commercial License Usage
 * ------------------------
 * Licensees holding valid commercial Deviare In-Proc licenses may use this
 * file in accordance with the commercial license agreement provided with the
 * Software or, alternatively, in accordance with the terms contained in
 * a written agreement between you and Nektra.  For licensing terms and
 * conditions see http://www.nektra.com/licensing/.  For further information
 * use the contact form at http://www.nektra.com/contact/.
 *
 *
 * GNU General Public License Usage
 * --------------------------------
 * Alternatively, this file may be used under the terms of the GNU
 * General Public License version 3.0 as published by the Free Software
 * Foundation and appearing in the file LICENSE.GPL included in the
 * packaging of this file.  Please review the following information to
 * ensure the GNU General Public License version 3.0 requirements will be
 * met: http://www.gnu.org/copyleft/gpl.html.
 *
 **/

typedef [v1_enum] enum eNktDispIds {
  dispidNktHookLibHook = 1,
  dispidNktHookLibRemoteHook,
  dispidNktHookLibUnhook,
  dispidNktHookLibUnhookProcess,
  dispidNktHookLibUnhookAll,
  dispidNktHookLibEnableHook,
  dispidNktHookLibSuspendThreadsWhileHooking,
  dispidNktHookLibShowDebugOutput,
  dispidNktHookLibRemoveHook,
  dispidNktHookLibGetModuleBaseAddress,
  dispidNktHookLibGetRemoteModuleBaseAddress,
  dispidNktHookLibGetProcedureAddress,
  dispidNktHookLibGetRemoteProcedureAddress,
  dispidNktHookLibCreateProcessWithDll,
  dispidNktHookLibCreateProcessWithLogonAndDll,
  dispidNktHookLibCreateProcessWithTokenAndDll,
  dispidNktHookLibInjectDll,
  dispidNktHookLibInjectDllH,
  //----
  dispidNktHookInfoId = 1,
  dispidNktHookInfoOrigProcAddr,
  dispidNktHookInfoNewProcAddr,
  dispidNktHookInfoCallOriginal,
  //----
  dispidNktHookProcessInfoProcess = 1,
  dispidNktHookProcessInfoThread,
  dispidNktHookProcessInfoProcessId,
  dispidNktHookProcessInfoThreadId
} eNktDispIds;
